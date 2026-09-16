// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature15Presentation",
    products: [.library(name: "Feature15Presentation", targets: ["Feature15Presentation"])],
    dependencies: [.package(path: "../Feature15Domain"),
        .package(path: "../Feature15Data")],
    targets: [.target(name: "Feature15Presentation", dependencies: [.product(name: "Feature15Domain", package: "Feature15Domain"), .product(name: "Feature15Data", package: "Feature15Data")])]
)
