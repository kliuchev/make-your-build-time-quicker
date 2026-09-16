// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature14Presentation",
    products: [.library(name: "Feature14Presentation", targets: ["Feature14Presentation"])],
    dependencies: [.package(path: "../Feature14Domain"),
        .package(path: "../Feature14Data")],
    targets: [.target(name: "Feature14Presentation", dependencies: [.product(name: "Feature14Domain", package: "Feature14Domain"), .product(name: "Feature14Data", package: "Feature14Data")])]
)
