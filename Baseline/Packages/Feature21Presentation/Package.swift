// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature21Presentation",
    products: [.library(name: "Feature21Presentation", targets: ["Feature21Presentation"])],
    dependencies: [.package(path: "../Feature21Domain"),
        .package(path: "../Feature21Data")],
    targets: [.target(name: "Feature21Presentation", dependencies: [.product(name: "Feature21Domain", package: "Feature21Domain"), .product(name: "Feature21Data", package: "Feature21Data")])]
)
