// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature33Presentation",
    products: [.library(name: "Feature33Presentation", targets: ["Feature33Presentation"])],
    dependencies: [.package(path: "../Feature33Domain"),
        .package(path: "../Feature33Data")],
    targets: [.target(name: "Feature33Presentation", dependencies: [.product(name: "Feature33Domain", package: "Feature33Domain"), .product(name: "Feature33Data", package: "Feature33Data")])]
)
