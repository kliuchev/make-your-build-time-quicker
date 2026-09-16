import Feature24Domain

public enum Feature24DataRepository {
    public static func load(_ id: Int) -> Feature24DomainModel {
        Feature24DomainModel(id: id, title: "Feature 24")
    }
}
